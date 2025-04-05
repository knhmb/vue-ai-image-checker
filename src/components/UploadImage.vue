<template>
  <div class="container">
    <div class="card">
      <h2>AI Image Copyright Checker</h2>

      <input type="file" @change="onFileChange" class="file-input" />

      <div v-if="previewUrl" class="preview-box">
        <img :src="previewUrl" alt="Preview" />
      </div>

      <button @click="uploadImage" :disabled="!image || loading" class="submit-btn">Upload</button>

      <loading-spinner v-if="loading"></loading-spinner>
      <p v-if="error" class="error">{{ error }}</p>

      <div
        v-if="result && !loading"
        :class="`verdict-box ${result.verdict === 'No Issue' ? 'verdict-good' : 'verdict-bad'}`"
      >
        <p><strong>Verdict:</strong> {{ result.verdict }}</p>
        <p><strong>Confidence:</strong> {{ result.confidence }}%</p>
      </div>
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

        if (data && data.verdict && data.confidence) {
          this.result = data
        } else {
          this.error = 'Unexpected response from server.'
        }
      } catch (error) {
        console.error('Upload failed:', error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  min-height: 100vh;
  background-color: #f4f6f8;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.card {
  background: #fff;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.card h2 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  text-align: center;
  color: #333;
}

.file-input {
  display: block;
  margin-bottom: 1rem;
}

.preview-box {
  margin: 1rem 0;
  border: 1px solid #ddd;
  padding: 0.5rem;
  border-radius: 0.5rem;
  text-align: center;
}

.preview-box img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
}

.error {
  color: red;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.submit-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem;
  width: 100%;
  border-radius: 0.5rem;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.verdict-box {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 0.5ren;
  font-size: 1rem;
}

.verdict-good {
  background-color: #e0f7e9;
  color: #207444;
}

.verdict-bad {
  background-color: #fde4e4;
  color: #b02020;
}
</style>
