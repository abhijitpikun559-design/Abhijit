import api from './api';

export const analyticsService = {
  getDashboard: async (userId) => {
    const response = await api.get(`/analytics/dashboard/${userId}`);
    return response.data;
  },

  getStudyHours: async (userId, days = 30) => {
    const response = await api.get(`/analytics/study-hours/${userId}`, {
      params: { days },
    });
    return response.data;
  },

  getQuizScores: async (userId, days = 30) => {
    const response = await api.get(`/analytics/quiz-scores/${userId}`, {
      params: { days },
    });
    return response.data;
  },

  getSubjectProgress: async (userId) => {
    const response = await api.get(`/analytics/subject-progress/${userId}`);
    return response.data;
  },

  getWeakTopics: async (userId, limit = 10) => {
    const response = await api.get(`/analytics/weak-topics/${userId}`, {
      params: { limit },
    });
    return response.data;
  },
};
