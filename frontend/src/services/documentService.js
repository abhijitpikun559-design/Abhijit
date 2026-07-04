import api from './api';

export const documentService = {
  uploadDocument: async (formData) => {
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  listDocuments: async (userId, subjectId = null) => {
    const response = await api.get('/documents/', {
      params: { user_id: userId, subject_id: subjectId },
    });
    return response.data;
  },

  getDocument: async (documentId) => {
    const response = await api.get(`/documents/${documentId}`);
    return response.data;
  },

  deleteDocument: async (documentId, userId) => {
    await api.delete(`/documents/${documentId}`, {
      params: { user_id: userId },
    });
  },

  updateDocument: async (documentId, userId, title, description) => {
    const response = await api.put(`/documents/${documentId}`, null, {
      params: { user_id: userId, title, description },
    });
    return response.data;
  },
};
