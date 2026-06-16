import mongoose from 'mongoose';

const researchSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  topic: {
    type: String,
    required: true,
  },
  status: {
    type: String,
    enum: ['pending', 'processing', 'completed', 'failed'],
    default: 'pending',
  },
  result: {
    type: String,
  },
  summary: {
    type: String,
  },
  summarySource: {
    type: String,
    enum: ['pipeline', 'python-rag', 'mistral', 'mistral-feedback', 'feedback'],
  },
  summaryGeneratedAt: {
    type: Date,
  },
  qualityScore: {
    type: Number,
  },
  userRating: {
    type: Number,
    min: 1,
    max: 5,
  },
  userFeedback: {
    type: String,
  },
  feedbackAt: {
    type: Date,
  },
  sessionId: {
    type: String,
  },
  completedAt: {
    type: Date,
  },
}, { timestamps: true });

const Research = mongoose.model('Research', researchSchema);
export default Research;
