<template>
  <div>
    <h1>Upload Image</h1>
    <div class="upload-container">
      <input type="file" @change="onFileChange" />
      <button @click="uploadImage" :disabled="!image || loading">Submit</button>
    </div>
    <p v-if="error" class="error-msg">{{ error }}</p>
    <div class="preview-content" v-if="previewUrl">
      <p>Preview:</p>
      <img :src="previewUrl" alt="Preview" />
    </div>
    <loading-spinner v-if="loading"></loading-spinner>
    <div v-if="result && !loading">
      <p><strong>Verdict:</strong> {{ result.verdict }}</p>
      <!-- <p><strong>Labels:</strong> {{ result.labels.join(', ') }}</p> -->
    </div>
  </div>
</template>

<script>
import LoadingSpinner from './LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner,
  },
  data() {
    return {
      image: null,
      result: null,
      error: '',
      previewUrl: null,
      loading: false,
    }
  },
  methods: {
    onFileChange(e) {
      console.log('file changed')

      const file = e.target.files[0]
      this.error = ''
      this.result = null
      this.previewUrl = null
      this.image = null

      if (!file) return

      if (!file.type.startsWith('image/')) {
        this.error = 'Please upload a valid image file.'
        this.image = null
        return
      }

      this.image = file
      this.previewUrl = URL.createObjectURL(file)
    },
    async uploadImage() {
      const formData = new FormData()
      formData.append('image', this.image)
      this.loading = true

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData,
        })

        const data = await response.json()

        this.result = data
        this.loading = false
      } catch (error) {
        this.loading = false
        console.error('Upload failed:', error)
      }
    },
  },
}
</script>

<style scoped>
.upload-container {
  display: flex;
}

.error-msg {
  color: red;
  font-size: 12px;
  margin: 0.5rem 0;
}

.preview-content img {
  width: 15rem;
}
</style>
