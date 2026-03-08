'use strict';

/**
 * Basic test suite for PlanIt skill.
 */

const { parse } = require('../src/parser');
const { handleMessage } = require('../src/index');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    console.log(`  ✓ ${label}`);
    passed++;
  } else {
    console.error(`  ✗ ${label}`);
    failed++;
  }
}

function section(name) {
  console.log(`\n── ${name} ──`);
}

// ─── Parser tests (sync) ─────────────────────────────────────────
section('Intent Parser');

{
  const r = parse('周五带爸妈去杭州');
  assert(r.destination === '杭州', '目的地识别: 杭州');
  assert(r.group === 'elderly', '人群识别: elderly (爸妈)');
  const d = new Date(r.departureDate);
  assert(d.getDay() === 5, '日期识别: 周五 (weekday=5)');
}

{
  const r = parse('明天去三亚玩3天，不要太贵');
  assert(r.destination === '三亚', '目的地: 三亚');
  assert(r.budget === 'budget', '预算: budget (不要太贵)');
  assert(r.duration === 3, '时长: 3天');
}

{
  const r = parse('下周末和老婆去丽江');
  assert(r.destination === '丽江', '目的地: 丽江');
  assert(r.group === 'couple', '人群: couple (老婆)');
}

{
  const r = parse('带孩子去成都玩两天');
  assert(r.destination === '成都', '目的地: 成都');
  assert(r.group === 'family_kids', '人群: family_kids (孩子)');
  assert(r.duration === 2, '时长: 两天');
}

{
  const r = parse('和朋友去西安，奢华体验');
  assert(r.destination === '西安', '目的地: 西安');
  assert(r.group === 'friends', '人群: friends (朋友)');
  assert(r.budget === 'luxury', '预算: luxury');
}

// ─── Async tests ──────────────────────────────────────────────────
async function runAsyncTests() {

  // ─── Itinerary generation ───────────────────────────────────────
  section('行程生成');

  {
    const userId = `test_${Date.now()}`;
    const result = await handleMessage({
      type: 'text',
      text: '周五带爸妈去杭州',
      userId,
      context: { originCity: '上海' },
    });

    assert(result.type === 'itinerary', '返回类型: itinerary');
    assert(result.summary.destination === '杭州', '目的地: 杭州');
    assert(Array.isArray(result.transport.outbound) && result.transport.outbound.length > 0, '包含出发交通');
    assert(Array.isArray(result.hotels) && result.hotels.length > 0, '包含酒店列表');
    assert(Array.isArray(result.timeline) && result.timeline.length > 0, '包含行程时间轴');
    assert(result.timeline[0].events.some(e => e.type === 'transport'), '第1天包含交通事件');
    assert(result.timeline[0].events.some(e => e.type === 'hotel_checkin'), '第1天包含入住事件');
    assert(Array.isArray(result.actions) && result.actions.length >= 2, '包含可操作按钮');

    // Check transport source
    const firstTrain = result.transport.outbound[0];
    if (firstTrain) {
      const src = firstTrain.source || 'mock';
      assert(['12306', 'mock'].includes(src), `交通数据来源合法: ${src}`);
      console.log(`     (交通来源: ${src})`);
    }
  }

  // ─── Personalization ────────────────────────────────────────────
  section('个性化 (预订历史重排)');

  {
    const userId = `pref_test_${Date.now()}`;

    const r1 = await handleMessage({ type: 'text', text: '周五带爸妈去杭州', userId, context: { originCity: '上海' } });
    assert(r1.type === 'itinerary', '首次查询返回行程');

    const targetHotel = r1.hotels[1] || r1.hotels[0];
    await handleMessage({
      type: 'action',
      action: 'book_hotel',
      userId,
      payload: {
        item: targetHotel,
        destination: '杭州',
        duration: 2,
        budget: 'mid',
        group: 'elderly',
      },
    });

    const r2 = await handleMessage({ type: 'text', text: '周五带爸妈去杭州', userId, context: { originCity: '上海' } });
    assert(r2.hotels[0].id === targetHotel.id, `已预订酒店 "${targetHotel.name}" 排到第一位`);
    assert(r2.hotels[0].previouslyBooked === true, '已预订酒店标记 previouslyBooked=true');
  }

  // ─── Edge cases ─────────────────────────────────────────────────
  section('边界情况');

  {
    const r = await handleMessage({ type: 'text', text: '', userId: 'u1' });
    assert(r.type === 'help', '空输入返回帮助');
  }

  {
    const r = await handleMessage({ type: 'text', text: '我想出去玩', userId: 'u1' });
    assert(r.type === 'clarification', '无目的地返回澄清请求');
  }

  {
    const r = await handleMessage({ type: 'action', action: 'book_hotel', userId: 'u1', payload: null });
    assert(r.type === 'error', '无效预订操作返回错误');
  }

  // ─── Summary ────────────────────────────────────────────────────
  console.log(`\n${'─'.repeat(40)}`);
  console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
  if (failed > 0) {
    process.exit(1);
  } else {
    console.log('✅ 所有测试通过！');
  }
}

runAsyncTests().catch((err) => {
  console.error('测试运行异常:', err);
  process.exit(1);
});
