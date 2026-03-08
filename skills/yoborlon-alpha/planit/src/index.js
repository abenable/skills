'use strict';

/**
 * PlanIt - 一句话规划出行
 * OpenClaw Skill Entry Point
 *
 * Handles two message types:
 *   1. plan   - User inputs a travel request → returns itinerary
 *   2. book   - User confirms a hotel booking → saves to storage and re-ranks
 */

const { parse } = require('./parser');
const { buildItinerary } = require('./itinerary');
const { recordHotelBooking, getPreferences, updatePreferences } = require('./storage');

/**
 * Handle an incoming OpenClaw skill message.
 *
 * @param {object} message - OpenClaw message object
 *   message.type        : 'text' | 'action'
 *   message.text        : string (for type='text')
 *   message.action      : string (for type='action', e.g. 'book_hotel')
 *   message.payload     : object (for type='action')
 *   message.userId      : string
 *   message.context     : object (optional, e.g. { originCity })
 *
 * @returns {Promise<object>} OpenClaw response object
 */
async function handleMessage(message) {
  const userId = message.userId || 'anonymous';
  const userPrefs = getPreferences(userId);
  const originCity = (message.context && message.context.originCity) || userPrefs.originCity || '上海';

  // --- Action: Hotel Booking ---
  if (message.type === 'action' && message.action === 'book_hotel') {
    const { item, destination, duration } = message.payload || {};
    if (!item || !destination) {
      return errorResponse('缺少预订信息，请重试。');
    }

    recordHotelBooking(userId, destination, item.id, {
      hotelName: item.name,
      duration,
      budget: message.payload.budget,
      group: message.payload.group,
      date: new Date().toISOString(),
    });

    return {
      type: 'confirmation',
      title: '预订记录已保存',
      message: `已记录您对【${item.name}】的偏好。下次搜索${destination}时将优先推荐此酒店。`,
      hotel: item,
      actions: [],
    };
  }

  // --- Action: Transport Booking ---
  if (message.type === 'action' && message.action === 'book_transport') {
    const { item } = message.payload || {};
    if (!item) return errorResponse('缺少交通信息，请重试。');
    return {
      type: 'confirmation',
      title: '交通已选定',
      message: `已记录您的出行方式：${item.name}，${item.from} → ${item.to}，${item.date} ${item.departureTime} 出发。`,
      transport: item,
      actions: [],
    };
  }

  // --- Text: Travel Planning Request ---
  const text = (message.text || '').trim();
  if (!text) {
    return helpResponse();
  }

  // Parse intent
  const intent = parse(text, originCity);

  // Validate destination
  if (!intent.destination) {
    return {
      type: 'clarification',
      title: '请告诉我目的地',
      message: `我没有识别到目的地，请告诉我您想去哪里？\n\n例如：\n• 周五带爸妈去杭州\n• 下周末两个人去成都，不要太贵\n• 明天去三亚玩3天`,
      suggestions: ['杭州', '成都', '北京', '三亚', '丽江', '西安'],
      actions: [],
    };
  }

  // Build itinerary (async: fetches real 12306 data)
  const itinerary = await buildItinerary(intent, userId);

  // Update origin city preference
  updatePreferences(userId, { originCity });

  return itinerary;
}

/**
 * Error response helper.
 */
function errorResponse(msg) {
  return {
    type: 'error',
    message: msg,
    actions: [],
  };
}

/**
 * Help response for empty input.
 */
function helpResponse() {
  return {
    type: 'help',
    title: 'PlanIt · 一句话规划出行',
    message: '您好！我是 PlanIt，只需一句话，我就能为您规划完整的出行行程。',
    examples: [
      '周五带爸妈去杭州',
      '下周末两个人去成都，不要太贵',
      '明天去三亚玩3天',
      '这个周末去北京，全家出行',
      '五一去丽江',
    ],
    actions: [],
  };
}

// --- CLI runner for testing ---
if (require.main === module) {
  (async () => {
    const args = process.argv.slice(2);
    const text = args.join(' ') || '周五带爸妈去杭州';
    const userId = 'test_user_001';

    console.log(`\n🗺️  PlanIt - 一句话规划出行`);
    console.log(`📝 输入: "${text}"\n`);

    const result = await handleMessage({
      type: 'text',
      text,
      userId,
      context: { originCity: '上海' },
    });

    console.log(JSON.stringify(result, null, 2));

    // Simulate booking the top hotel
    if (result.type === 'itinerary' && result.hotels && result.hotels[0]) {
      const topHotel = result.hotels[0];
      console.log(`\n✅ 模拟预订酒店: ${topHotel.name}`);

      const bookResult = await handleMessage({
        type: 'action',
        action: 'book_hotel',
        userId,
        payload: {
          item: topHotel,
          destination: result.summary.destination,
          duration: result.summary.duration,
          budget: result.summary.budget,
          group: result.summary.group,
        },
      });
      console.log(JSON.stringify(bookResult, null, 2));

      // Re-run same query to verify personalization
      console.log(`\n🔄 再次查询 "${text}" (验证个性化排序):`);
      const result2 = await handleMessage({
        type: 'text',
        text,
        userId,
        context: { originCity: '上海' },
      });
      if (result2.hotels && result2.hotels[0]) {
        console.log(`\n🏨 酒店排序（预订后）:`);
        result2.hotels.forEach((h, i) => {
          const mark = h.previouslyBooked ? ' ★ 上次选择' : '';
          console.log(`  ${i + 1}. ${h.name} ¥${h.pricePerNight}/晚${mark}`);
        });
      }

      // Show transport source
      if (result.transport && result.transport.outbound[0]) {
        const t = result.transport.outbound[0];
        console.log(`\n🚄 交通数据来源: ${t.source || 'mock'}`);
        if (t.source === '12306') {
          console.log(`   ${t.trainNo}  ${t.departureTime} → ${t.arrivalTime}  (${t.durationLabel})`);
        }
      }
    }
  })().catch(console.error);
}

module.exports = { handleMessage };
