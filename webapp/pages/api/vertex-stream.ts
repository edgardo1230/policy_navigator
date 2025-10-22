
import { NextApiRequest, NextApiResponse } from "next";
import { GoogleAuth } from "google-auth-library";
import path from "path";

export const config = {
  api: {
    bodyParser: false, // For streaming
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end("Method Not Allowed");
    return;
  }
  try {
    const keyPath = path.join(process.cwd(), "service-account.json");
    const auth = new GoogleAuth({
      keyFile: keyPath,
      scopes: ["https://www.googleapis.com/auth/cloud-platform"],
    });
    const client = await auth.getClient();
  const apiUrl = "https://us-central1-aiplatform.googleapis.com/v1/projects/qwiklabs-gcp-01-f81085004973/locations/us-central1/reasoningEngines/1235310109899358208:streamQuery?alt=sse";

    // Collect the raw body
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
    });
    req.on("end", async () => {
      try {
        const response = await client.request({
          url: apiUrl,
          method: "POST",
          data: JSON.parse(body),
          responseType: "stream",
          headers: {
            "Content-Type": "application/json",
          },
        });

        res.writeHead(200, {
          "Content-Type": response.headers.get
            ? response.headers.get("content-type") || "application/json"
            : "application/json",
        });
        // @ts-ignore
        response.data.pipe(res);
      } catch (error: any) {
        res.status(500).json({ error: error.message || "Vertex AI stream call failed" });
      }
    });
  } catch (error: any) {
    res.status(500).json({ error: error.message || "Vertex AI stream call failed" });
  }
}
