import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import { useEffect } from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

export default function ChatPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!session && status !== "loading") {
      router.replace("/login");
    }
  }, [session, status, router]);

  if (!session) {
    return null;
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to the Chat, {session.user?.name}
      </Typography>
      {/* Chat UI goes here */}
    </Container>
  );
}
