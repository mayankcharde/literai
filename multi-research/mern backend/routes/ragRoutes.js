import express from 'express';
import { setupRag, askQuestion, getRagStats } from '../controllers/ragController.js';
import { protect } from '../middleware/authMiddleware.js';

const router = express.Router();

router.post('/setup', protect, setupRag);
router.post('/ask', protect, askQuestion);
router.get('/stats', protect, getRagStats);

export default router;
