const connections = new Map(); 
const submissions = new Map(); 
function registerConnection(submissionId, res) {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive',
  });
  res.write(':\n\n'); // initial comment to open the stream immediately

  // auto-cleanup if nothing arrives 
  const timeout = setTimeout(() => {
    sendEvent(submissionId, { status: 'timeout', message: 'No response received' });
  }, 15_000); //15sec

  connections.set(submissionId, { res, timeout });

  res.on('close', () => {
    clearTimeout(timeout);
    connections.delete(submissionId);
  });
}

function sendEvent(submissionId, data) {
  const conn = connections.get(submissionId);
  if (!conn){
    console.warn(`No active connection for submissionId: ${submissionId}. Storing data for later retrieval.`);
    submissions.set(submissionId, data);
    return;
  }

  clearTimeout(conn.timeout);
  conn.res.write(`event: result\ndata: ${JSON.stringify(data)}\n\n`);
  conn.res.end();
  connections.delete(submissionId);
}

module.exports = { registerConnection, sendEvent , submissions };