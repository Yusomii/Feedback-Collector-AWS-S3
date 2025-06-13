const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, ScanCommand } = require("@aws-sdk/lib-dynamodb");

const client = new DynamoDBClient({});
const dynamodb = DynamoDBDocumentClient.from(client);

// IMPORTANT: Your TABLE_NAME environment variable should be passed from the SAM template, not hardcoded.
// If your SAM template defines it, you should access it like this:
const TABLE_NAME = process.env.TABLE_NAME;
// If you are absolutely sure 'Feedback' is the name and not from env var, keep it, but it's less flexible.
// const TABLE_NAME = 'Feedback'; // Original line if not using env var

exports.handler = async (event) => { // Changed 'export const handler' to 'exports.handler'
  try {
    const command = new ScanCommand({ TableName: TABLE_NAME });
    const data = await dynamodb.send(command);

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,GET"
      },
      body: JSON.stringify(data.Items),
    };
  } catch (err) {
    console.error("Error fetching feedback:", err);
    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,GET"
      },
      body: JSON.stringify({ message: "Could not fetch feedback", details: err.message }),
    };
  }
};