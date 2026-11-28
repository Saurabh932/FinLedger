import api from '../lib/api'

export const registerUser = async (userData) => {
    const response = await api.post('/auth/register', userData)

    return response.data
}