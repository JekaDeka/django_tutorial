import ApiService from './api.service.js'

const BlogService = {
  getPosts(payload) {
    return ApiService.query('posts', {
      params: payload
    })
  },
  getPost(payload) {
    return ApiService.get('posts', payload)
  },
  savePost(payload) {
    if (payload.id !== null) {
      return ApiService.put(`posts/${payload.id}`, payload)
    } else return ApiService.post('posts', payload)
  },
  deletePost(payload) {
    return ApiService.delete(`posts/${payload}`)
  }
}
export default BlogService
