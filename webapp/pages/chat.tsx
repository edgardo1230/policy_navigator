
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import { useEffect, useState, useRef } from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";

export default function ChatPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [messages, setMessages] = useState<{ user: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!session && status !== "loading") {
      router.replace("/login");
    }
  }, [session, status, router]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (!session) {
    return null;
  }

  // Helper to get Google access token from session
  const getAccessToken = () => {
    // next-auth stores tokens in session, but Google access token may be in session.accessToken or session.idToken
    // You may need to adjust this depending on your next-auth config
    // Try session.accessToken, session.idToken, or session.token
    // For Google, usually session.accessToken
    // @ts-ignore
    return session?.accessToken || "";
  };

  const handleSend = async () => {
    if (input.trim() === "" || loading) return;
    setMessages([...messages, { user: session.user?.name || "Me", text: input }]);
    setInput("");
    setLoading(true);

    try {
  const apiUrl = "/api/vertex-stream";
      const payload = {
        class_method: "stream_query",
        input: {
          user_id: session.user?.email || "user",
          session_id: sessionId,
          message: input,
        },
      };

      const res = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const responseJson = await res.json();
      // Handle error responses (e.g., MODEL_ARMOR)
      let aiMessage = "No response.";
      if (responseJson && responseJson.error_code === "MODEL_ARMOR") {
        aiMessage = `Blocked by Responsible AI: ${responseJson.error_message}`;
      } else if (responseJson && responseJson.content && responseJson.content.parts && responseJson.content.parts.length > 0) {
        aiMessage = responseJson.content.parts[0].text;
      }

      setMessages(msgs => [...msgs, { user: "AI", text: aiMessage }]);
    } catch (err) {
      setMessages(msgs => [...msgs, { user: "AI", text: "Error contacting reasoning engine." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to the Chat, {session.user?.name}
      </Typography>
      <Paper elevation={3} sx={{ p: 2, mb: 2, minHeight: 300, maxHeight: 400, overflowY: "auto" }}>
        {messages.map((msg, idx) => (
          <Box key={idx} sx={{ mb: 1 }}>
            <Typography variant="subtitle2" color={msg.user === "AI" ? "secondary" : "primary"}>
              {msg.user}:
            </Typography>
            <Typography variant="body1">{msg.text}</Typography>
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </Paper>
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder={loading ? "Waiting for response..." : "Type your message..."}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === "Enter") handleSend();
          }}
          disabled={loading}
        />
        <Button variant="contained" color="primary" onClick={handleSend} disabled={loading}>
          Send
        </Button>
      </Box>
    </Container>
  );
}
