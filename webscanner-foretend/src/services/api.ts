import axios from 'axios';

const API_URL = 'http://47.254.23.221/api';

//登陆
export const login = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

//注册
export const register = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/register`, { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};
//更新信息
export const changePwd = async (id: number,email: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/saveInfo`, { id,email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

//漏洞扫描
export const startScan = async (url: string, config: string) => {
  try {
    const response = await axios.post(`${API_URL}/scan`, { url, config });
    console.log(response)
    return response.data; // 返回响应数据，包括 results 和 url
  } catch (error) {
    throw error;
  }
};

//漏洞信息
export const vulInfo = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/vulInfo`, { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

//仪表盘
export const dashboard = async () => {
  try {
    const response = await axios.get(`${API_URL}/dashboard`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
//钓鱼网站识别
export const checkUrl = async (url:string) => {
  try {
    const response = await axios.post(`${API_URL}/check-url`, { url });
    return response.data.isPhishing;
  } catch (error) {
    console.error('Error checking URL:', error);
    throw error;
  }
};
//图片识别
export const checkImage = async (image:File) => {
  const formData = new FormData();
  formData.append('image', image);

  try {
    const response = await axios.post(`${API_URL}/check-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.isPhishing;
  } catch (error) {
    console.error('Error checking image:', error);
    throw error;
  }
};
//保存设置
export const saveInfo = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${API_URL}/saveInfo`, { email, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};