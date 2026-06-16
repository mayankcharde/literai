/**
 * Batch-generate summaries for completed research missing a summary field.
 * Usage: node scripts/migrateSummaries.js
 */
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import path from 'path';
import { fileURLToPath } from 'url';
import Research from '../models/Research.js';
import { generateResearchSummary } from '../services/summaryService.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '..', '.env') });

const BATCH_DELAY_MS = 1500;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function migrate() {
  if (!process.env.MONGO_URI) {
    console.error('MONGO_URI is required');
    process.exit(1);
  }

  await mongoose.connect(process.env.MONGO_URI);
  console.log('Connected to MongoDB');

  const query = {
    status: 'completed',
    result: { $exists: true, $nin: [null, ''] },
    $or: [{ summary: { $exists: false } }, { summary: null }, { summary: '' }],
  };

  const items = await Research.find(query).sort({ createdAt: 1 });
  console.log(`Found ${items.length} research record(s) needing summaries`);

  let success = 0;
  let failed = 0;

  for (const research of items) {
    try {
      console.log(`Processing: ${research._id} — ${research.topic.slice(0, 60)}...`);
      const { summary, source } = await generateResearchSummary({
        sessionId: research.sessionId,
        report: research.result,
        topic: research.topic,
      });
      research.summary = summary;
      research.summarySource = source;
      research.summaryGeneratedAt = new Date();
      await research.save();
      success += 1;
      console.log(`  ✓ Summary saved (${source}, ${summary.split(/\s+/).length} words)`);
    } catch (err) {
      failed += 1;
      console.error(`  ✗ Failed: ${err.message}`);
    }
    await sleep(BATCH_DELAY_MS);
  }

  console.log(`\nDone. Success: ${success}, Failed: ${failed}`);
  await mongoose.disconnect();
}

migrate().catch((err) => {
  console.error(err);
  process.exit(1);
});
