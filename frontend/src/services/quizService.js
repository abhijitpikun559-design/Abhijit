import api from './api';

export const quizService = {
  generateQuiz: async (documentId, difficulty = 'medium', numQuestions = 10) => {
    const response = await api.post('/quiz/generate', {
      document_id: documentId,
      difficulty,
      num_questions: numQuestions,
    });
    return response.data;
  },

  getQuiz: async (quizId) => {
    const response = await api.get(`/quiz/${quizId}`);
    return response.data;
  },

  submitQuiz: async (quizId, responses, userId) => {
    const response = await api.post(`/quiz/${quizId}/submit`, {
      quiz_id: quizId,
      responses,
      user_id: userId,
    });
    return response.data;
  },

  getQuizHistory: async (userId, limit = 10) => {
    const response = await api.get(`/quiz/history/${userId}`, {
      params: { limit },
    });
    return response.data;
  },
};
