import api from './api';

export const flashcardService = {
  generateFlashcards: async (documentId, userId) => {
    const response = await api.post('/flashcards/generate', null, {
      params: { document_id: documentId, user_id: userId },
    });
    return response.data;
  },

  createFlashcard: async (flashcard, userId) => {
    const response = await api.post('/flashcards/', flashcard, {
      params: { user_id: userId },
    });
    return response.data;
  },

  getUserFlashcards: async (userId, limit = 50) => {
    const response = await api.get(`/flashcards/user/${userId}`, {
      params: { limit },
    });
    return response.data;
  },

  markKnown: async (flashcardId, userId) => {
    const response = await api.put(`/flashcards/${flashcardId}/mark-known`, null, {
      params: { user_id: userId },
    });
    return response.data;
  },

  markRevision: async (flashcardId, userId) => {
    const response = await api.put(`/flashcards/${flashcardId}/mark-revision`, null, {
      params: { user_id: userId },
    });
    return response.data;
  },

  deleteFlashcard: async (flashcardId, userId) => {
    await api.delete(`/flashcards/${flashcardId}`, {
      params: { user_id: userId },
    });
  },
};
