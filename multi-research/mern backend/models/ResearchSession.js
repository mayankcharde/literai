import mongoose from 'mongoose';

const researchSessionSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  researchId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Research',
    required: true,
  },
  sessionData: [{
    question: String,
    answer: String,
    confidence: Number,
    sources: [String],
    timestamp: {
      type: Date,
      default: Date.now
    }
  }]
}, { timestamps: true });

const ResearchSession = mongoose.model('ResearchSession', researchSessionSchema);
export default ResearchSession;
