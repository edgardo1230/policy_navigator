import { signIn, useSession } from "next-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/router";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

export default function LoginPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (session) {
      router.replace("/chat");
    }
  }, [session, router]);

  return (
    <Container maxWidth="sm" sx={{ mt: 8, textAlign: "center" }}>
      <Typography variant="h4" gutterBottom>
        Sign in to start chatting
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => signIn("google")}
        sx={{ mt: 4 }}
      >
        Sign in with Google
      </Button>
    </Container>
  );
}
