import express from 'express';
import {
  startResearch,
  getResearchHistory,
  getResearch,
  getResearchSummary,
  submitResearchFeedback,
  deleteResearch,
  getResearchStats,
} from '../controllers/researchController.js';
import { protect } from '../middleware/authMiddleware.js';

const router = express.Router();

router.get('/stats', protect, getResearchStats);
router.get('/history', protect, getResearchHistory);
router.get('/summary/:id', protect, getResearchSummary);
router.post('/start', protect, startResearch);
router.post('/:id/feedback', protect, submitResearchFeedback);
router.get('/:id', protect, getResearch);
router.delete('/:id', protect, deleteResearch);

export default router;
