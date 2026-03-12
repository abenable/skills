#!/usr/bin/env node

const http = require('http');

function request(path, method = 'GET', body = null, token = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8080,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (token) {
      options.headers['Authorization'] = 'Bearer ' + token;
    }
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });
    
    req.on('error', reject);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

const auth_register = async function(args) {
  return request('/api/auth/register', 'POST', args);
};

const auth_login = async function(args) {
  const result = await request('/api/auth/login', 'POST', args);
  return result;
};

const get_users = async function(args) {
  const role = args && args.role;
  const path = role ? '/api/users?role=' + encodeURIComponent(role) : '/api/users';
  return request(path);
};

const get_product_managers = async function() {
  return request('/api/users/product-managers');
};

const get_projects = async function() {
  return request('/api/projects');
};

const create_project = async function(args) {
  return request('/api/projects', 'POST', args);
};

const get_my_tasks = async function() {
  return request('/api/tasks');
};

const create_task = async function(args) {
  const body = Object.assign({}, args, { status: '待处理' });
  return request('/api/tasks/agent/create', 'POST', body);
};

const update_task_status = async function(args) {
  const { taskId, status } = args;
  return request('/api/tasks/' + taskId + '/status', 'PUT', { status });
};

exports.auth_register = auth_register;
exports.auth_login = auth_login;
exports.get_users = get_users;
exports.get_product_managers = get_product_managers;
exports.get_projects = get_projects;
exports.create_project = create_project;
exports.get_my_tasks = get_my_tasks;
exports.create_task = create_task;
exports.update_task_status = update_task_status;
