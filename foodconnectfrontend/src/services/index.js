import axios from 'axios';
/**
 * FoodConnect
 * @type {AxiosInstance}
 */

const customAxios = axios.create({
  baseURL: 'http://localhost:8000/app',
});

customAxios.interceptors.request.use(
  async (request) => {
    const AccessToken = await localStorage.getItem('AccessToken');
    const RefreshToken = await localStorage.getItem('RefreshToken');
    request.headers['AccessToken'] = `${AccessToken}`;
    request.headers['RefreshToken'] = `${RefreshToken}`;
    return Promise.resolve(request);
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default customAxios;
