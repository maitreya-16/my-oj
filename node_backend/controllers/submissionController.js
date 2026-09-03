const axios = require('axios');  
const CELERY_API_BASE = process.env.FLASK_API_BASE;
const { Submission } = require('../models');
const { registerConnection , submissions } = require('./sse');

async function enqueueTask(queue, data) {
    try {
        // if (data.code)
            // data.code = Buffer.from(data.code).toString('base64');
        // if (data.customTestcase)
        //     data.customTestcase = Buffer.from(data.customTestcase).toString('base64');

        let endpoint = '';
        if (queue === 'submitQueue') endpoint = '/enqueue/submit';
        else if (queue === 'runQueue') endpoint = '/enqueue/run';
        else if (queue === 'runSystemQueue') endpoint = '/enqueue/system';

        const res = await axios.post(`${CELERY_API_BASE}${endpoint}`, data);
        // console.log(`Enqueued via Flask: ${res.data.message}`);
    } catch (error) {
        console.error(`Error enqueueing via Flask API:`, error.message);
    }
}

exports.sseRegister = (req, res) => {
    let { submission_id } = req.params;

    submission_id = String(submission_id);

    if (!submission_id) {
        return res.status(400).json({ error: 'submission_id is required' });
    }

    if (submissions.has(submission_id)) {
        const submissionData = submissions.get(submission_id);

        submissions.delete(submission_id); // Remove after sending to avoid duplicate sends

        return res.status(200).json(submissionData);
    }

    registerConnection(submission_id, res);
}

exports.RunProblem = async (req, res) => {
try {

        const { problem_id, code, customTestcase, language } = req.body;
        const user = req.user;
        
        const submission_id= `run_${Date.now()}`;

        const runData = {
            submission_id: submission_id,
            problem_id,
            // team_id: user.team_id,
            code,
            customTestcase: customTestcase || "",
            language,
        };

        await enqueueTask('runQueue', runData);

        res.status(200).json({ message: `Run request enqueued successfully.`,submission_id: submission_id });
    }catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Failed to enqueue run request.' });
    }   
}

exports.RunOnSystem = async (req, res) => {
  try {
    const { problem_id, customTestcase } = req.body;
    const { problem, event } = req;

    const submission_id = `system_${Date.now()}`;

    const runData = {
      submission_id,
      problem_id,
      customTestcase: customTestcase || "",
    };

    await enqueueTask("runSystemQueue", runData);

    return res.status(200).json({
      message: "Run request has been successfully enqueued.",
      submission_id,
    });
  } catch (error) {
    console.error("Error enqueuing run request:", error);
    return res
      .status(500)
      .json({ error: "Unable to enqueue run request. Please try again." });
  }
};

exports.SubmitProblem = async (req, res) => {
    try {
        const { problem_id, code, language } = req.body;
        const team_id = req.user.team_id;
        const event_id = req.user.event_id;
        const teamname = req.user.teamname
        console.log("Event_id",event_id);
        const submission = await Submission.create({
            teamname,
            team_id,
            problem_id,
            event_id: event_id,
            code,
            language,
            result: 'Pending',
        });
        const SubmissionData = {
            submission_id: submission.id,
            code,
            language,
            problem_id,
        };

        await enqueueTask('submitQueue', SubmissionData)
        res.status(200).json({ message: 'Code submitted successfully, waiting for evaluation.', submission_id: submission.id, result: submission.result });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error submitting code', details: error.message });
    }
}


