import { PredictionServiceClient } from '@google-cloud/aiplatform';
import { NextApiRequest, NextApiResponse } from 'next';

// Configuration for the Vertex AI client
if (!process.env.GCP_CREDENTIALS_JSON) {
  throw new Error(
    'GCP_CREDENTIALS_JSON environment variable not set. Please provide the service account key as a JSON string.'
  );
}

// Configuration for the Vertex AI client
const clientOptions = {
  // Your model's endpoint region
  apiEndpoint: 'us-central1-aiplatform.googleapis.com',
  // Parse the credentials directly from the environment variable
  credentials: JSON.parse(process.env.GCP_CREDENTIALS_JSON),
};

// Initialize the client
const predictionServiceClient = new PredictionServiceClient(clientOptions);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    // TODO: Replace with your actual project, location, and endpoint ID
    const endpoint = `projects/your-gcp-project-id/locations/us-central1/endpoints/your-endpoint-id`;

    const instances = [{ content: prompt }];
    const parameters = {
      temperature: 0.2,
      maxOutputTokens: 256,
      topP: 0.95,
      topK: 40,
    };

    const request = {
      endpoint,
      instances,
      parameters,
    };

    // Make the API call to Vertex AI
    const [response] = await predictionServiceClient.predict(request);

    // TODO: Process the response as needed
    const prediction = response.predictions?.[0];

    res.status(200).json({ prediction });
  } catch (error) {
    console.error('Error calling Vertex AI:', error);
    res.status(500).json({ error: 'Failed to invoke Vertex AI agent' });
  }
}
