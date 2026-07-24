// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/components/AuthProvider";

export const metadata: Metadata = {
    title: "Governance & Disaster Case-Study Simulator",
    description: "Analyze real crises, propose your response, get critiqued against reality.",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className="bg-slate-950 text-white min-h-screen">
                <AuthProvider>{children}</AuthProvider>
            </body>
        </html>
    );
}
