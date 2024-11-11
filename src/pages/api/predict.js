import { model } from '@/lib/model'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  try {
    const { prompt } = req.body

    if (!prompt) {
      return res.status(400).json({
        error: "Missing 'prompt' in request body"
      })
    }

    const prediction = await model.predict(prompt)

    return res.status(200).json({
      status: 'success',
      prediction
    })
  } catch (error) {
    console.error('Prediction error:', error)
    return res.status(500).json({
      status: 'error',
      message: error.message
    })
  }
} 