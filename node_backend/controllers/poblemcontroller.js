const Problem = require('../models/Problem');
const ProblemSample = require('../models/ProblemSample');
const sequelize = require('../config/database');

// Create new Problem (with optional samples)
exports.createProblem = async (req, res) => {
  try {
    const { title, description, score, input_format, output_format, constraints, isjunior, time_limit, memory_limit, event_id, samples } = req.body;

    // create problem first
    const problem = await Problem.create({ title, description, score, input_format, output_format, constraints, isjunior, time_limit, memory_limit, event_id, });
    // const missingFields = problem.filter(field => !(field in req.body));

    // if (missingFields.length > 0) {
    //   return res.status(400).json({
    //     error: "Missing required fields",
    //     missing: missingFields
    //   });
    // }

    // if samples are provided, bulk insert them
    if (samples && Array.isArray(samples)) {
      const formattedSamples = samples.map(s => ({
        problem_id: problem.id,
        input: s.input,
        output: s.output,
        explanation: s.explanation || null
      }));
      await ProblemSample.bulkCreate(formattedSamples);
    }

    return res.status(201).json({ message: "Problem created", problem });
  } catch (err) {
    console.error(err);
    return res.status(500).json({
      error: "Failed to create problem"
      , details: err.message
    });
  }
};

// Get all problems with their samples
exports.getAllProblems = async (req, res) => {

  try {
    const { event_id, isjunior } = req.user;
    const problems = await Problem.findAll({
      where: { event_id, isjunior },
      include: [{ model: ProblemSample, as: "samples" }]
    });
    return res.json(problems);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to fetch problems" });
  }
};

// Get a single problem by ID
exports.getProblemById = async (req, res) => {
  try {
    const { id } = req.params;
    const problem = await Problem.findByPk(id, {
      include: [{ model: ProblemSample, as: "samples" }]
    });

    if (!problem) return res.status(404).json({ error: "Problem not found" });

    return res.json(problem);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to fetch problem" });
  }
};

// Add a sample test case to a problem
exports.addSample = async (req, res) => {
  try {
    const { id } = req.params; // problem ID
    const { input, output, explanation } = req.body;
    //     const data = req.body();
    // const missingFields = data.filter(field => !(field in req.body));

    //     if (missingFields.length > 0) {
    //       return res.status(400).json({
    //         error: "Missing required fields",
    //         missing: missingFields
    //       });
    //     }

    const problem = await Problem.findByPk(id);
    if (!problem) return res.status(404).json({ error: "Problem not found" });

    const sample = await ProblemSample.create({
      problem_id: id,
      input,
      output,
      explanation
    });

    return res.status(201).json({ message: "Sample added", sample });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to add sample" });
  }
};

// Delete a problem (samples deleted automatically via CASCADE)
exports.deleteProblem = async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await Problem.destroy({ where: { id } });

    if (!deleted) return res.status(404).json({ error: "Problem not found" });

    return res.json({ message: "Problem deleted" });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to delete problem" });
  }
};

exports.updateProblem = async (req, res) => {
  try {
    const { id } = req.params;
    const {
      title,
      description,
      score,
      input_format,
      output_format,
      constraints,
      isjunior,
      time_limit,
      memory_limit,
      event_id,
      samples
    } = req.body;

    const problem = await Problem.findByPk(id);
    if (!problem) {
      return res.status(404).json({ error: `Problem with ID ${id} not found` });
    }

    // partial update (only update if field is provided)
    problem.title = title || problem.title;
    problem.description = description || problem.description;
    problem.score = score || problem.score;
    problem.input_format = input_format || problem.input_format;
    problem.output_format = output_format || problem.output_format;
    problem.constraints = constraints || problem.constraints;
    problem.isjunior = (isjunior !== undefined) ? isjunior : problem.isjunior;
    problem.time_limit = time_limit || problem.time_limit;
    problem.memory_limit = memory_limit || problem.memory_limit;
    problem.event_id = event_id || problem.event_id;

    await problem.save();

    // handle samples if provided
    if (samples && Array.isArray(samples)) {
      // delete old samples
      await ProblemSample.destroy({ where: { problem_id: id } });

      // add new ones
      const formattedSamples = samples.map(s => ({
        problem_id: id,
        input: s.input,
        output: s.output,
        explanation: s.explanation || null
      }));

      await ProblemSample.bulkCreate(formattedSamples);
    }

    return res.status(200).json({
      message: "Problem updated successfully",
      problem
    });

  } catch (error) {
    console.error(error);
    return res.status(500).json({
      error: "Error updating problem",
      details: error.message
    });
  }
};

exports.updateSample = async (req, res) => {
  try {
    const { id } = req.params; // sample ID from URL
    const { input, output, explanation } = req.body;

    const sample = await ProblemSample.findByPk(id);
    if (!sample) {
      return res.status(404).json({ error: `Sample with ID ${id} not found` });
    }

    // partial update (only update provided fields)
    sample.input = input || sample.input;
    sample.output = output || sample.output;
    sample.explanation = (explanation !== undefined) ? explanation : sample.explanation;

    await sample.save();

    return res.status(200).json({ message: "Sample updated successfully", sample });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to update sample" });
  }
};
// Delete a sample test case by sample ID
exports.deleteSample = async (req, res) => {
  try {
    const { id } = req.params;

    const deleted = await ProblemSample.destroy({ where: { id } });

    if (!deleted) {
      return res.status(404).json({ error: "Sample not found" });
    }

    return res.json({ message: "Sample deleted successfully" });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: "Failed to delete sample" });
  }
};

exports.getAllProblemsAccuracy = async (req, res) => {
  try {
    const isJunior = req.user.isjunior;   // boolean
    const event_id = req.user.event_id;   // integer

    // Query to calculate accuracy = total accepted submissions / total submissions per problem
    const rows = await sequelize.query(`
      SELECT 
        p.id AS problem_id,
        COUNT(s.id) AS total_submissions,  -- total submissions for the problem
        COUNT(CASE WHEN s.result = 'accepted' THEN 1 END) AS accepted_submissions, -- accepted submissions
        CONCAT(
          ROUND(
            CASE WHEN COUNT(s.id) = 0 THEN 0
                 ELSE COUNT(CASE WHEN s.result = 'accepted' THEN 1 END) * 100.0 
                      / COUNT(s.id)
            END, 2
          ), '%'
        ) AS accuracy
      FROM problems p
      LEFT JOIN submissions s 
        ON s.problem_id = p.id 
        AND s.event_id = :eventId
      WHERE p.isjunior = :isJunior
        AND p.event_id = :eventId
      GROUP BY p.id
      ORDER BY p.id;
    `, {
      replacements: { isJunior, eventId: event_id },
      type: sequelize.QueryTypes.SELECT
    });

    return res.status(200).json(rows);
  } catch (error) {
    console.error("Error fetching problem accuracy:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
};

