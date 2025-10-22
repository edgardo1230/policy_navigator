// import { NextApiRequest, NextApiResponse } from "next";
// import { GoogleAuth } from "google-auth-library";
// import path from "path";

// export default async function handler(req: NextApiRequest, res: NextApiResponse) {
//   try {
//     const keyPath = path.join(process.cwd(), "service-account.json");
//     const auth = new GoogleAuth({
//       keyFile: keyPath,
//       scopes: ["https://www.googleapis.com/auth/cloud-platform"],
//     });
//     const client = await auth.getClient();
//     const projectId = "qwiklabs-gcp-01-f81085004973";
//     const location = "us-central1";
//     const modelId = "1235310109899358208"; // TODO: Replace with your actual model ID
//     const apiUrl = `https://us-central1-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/models/${modelId}:predict`;

//     const payload = req.body;

//     const result = await client.request({
//       url: apiUrl,
//       method: "POST",
//       data: payload,
//     });

//     res.status(200).json(result.data);
//   } catch (error: any) {
//     res.status(500).json({ error: error.message || "Vertex AI call failed" });
//   }
// }
