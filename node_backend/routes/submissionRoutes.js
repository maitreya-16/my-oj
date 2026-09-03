const express = require('express');
const router = express.Router();
const submissionController = require('../controllers/submissionController');
const validateSubmissionWindow = require('../middlewares/validateSubmission.js');
const auth = require('../middlewares/authMiddleware');

router.get('/sse/:submission_id', submissionController.sseRegister);

// router.post('/run',auth,validateSubmissionWindow,submissionController.RunProblem);
router.post('/run',submissionController.RunProblem);

// router.post('/run-system',auth,validateSubmissionWindow,submissionController.RunOnSystem);
router.post('/run-system',submissionController.RunOnSystem);

router.post('/submit',auth,validateSubmissionWindow,submissionController.SubmitProblem);
// router.post('/submit',submissionController.SubmitProblem);

module.exports = router;