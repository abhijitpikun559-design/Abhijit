import api from './api';

export const profileService = {
  getProfile: async (userId) => {
    const response = await api.get(`/profile/${userId}`);
    return response.data;
  },

  updateProfile: async (userId, updateData) => {
    const response = await api.put(`/profile/${userId}`, updateData);
    return response.data;
  },

  deleteAccount: async (userId) => {
    await api.delete(`/profile/${userId}`);
  },

  getStatistics: async (userId) => {
    const response = await api.get(`/profile/statistics/${userId}`);
    return response.data;
  },
};
