import api from './api';

export const searchService = {
  globalSearch: async (userId, query, searchType = 'all') => {
    const response = await api.get('/search/global', {
      params: { user_id: userId, query, search_type: searchType },
    });
    return response.data;
  },

  searchDocuments: async (userId, query) => {
    const response = await api.get('/search/documents', {
      params: { user_id: userId, query },
    });
    return response.data;
  },

  searchFlashcards: async (userId, query) => {
    const response = await api.get('/search/flashcards', {
      params: { user_id: userId, query },
    });
    return response.data;
  },
};
