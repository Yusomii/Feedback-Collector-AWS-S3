const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = 'Feedback';

exports.handler = async (event) => {
  try {
    const data = await dynamodb.scan({ TableName: TABLE_NAME }).promise();
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify(data.Items),
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Could not fetch feedback" }),
    };
  }
};
