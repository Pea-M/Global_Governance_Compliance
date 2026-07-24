"use client";

import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import { supabase } from "@/lib/supabase";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

export default function LoginPage() {
    const { session } = useAuth();
    const router = useRouter();

    // Once signed in, go to homepage
    useEffect(() => {
        if (session) {
            router.push("/");
        }
    }, [session, router]);

    return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                {/* Logo / Branding */}
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white tracking-tight">
                        Governance & Disaster Simulator
                    </h1>
                    <p className="mt-2 text-slate-400 text-sm">
                        Sign in to propose solutions, get critiqued, and track your progress.
                    </p>
                </div>

                {/* Supabase Auth UI */}
                <div className="bg-slate-900 border border-slate-700 rounded-xl p-8 shadow-2xl">
                    <Auth
                        supabaseClient={supabase}
                        appearance={{
                            theme: ThemeSupa,
                            variables: {
                                default: {
                                    colors: {
                                        brand: "#3b82f6",
                                        brandAccent: "#2563eb",
                                        inputBackground: "#1e293b",
                                        inputText: "#f1f5f9",
                                        inputLabelText: "#94a3b8",
                                        inputBorder: "#475569",
                                        inputBorderFocus: "#3b82f6",
                                        messageText: "#f1f5f9",
                                        messageBackground: "#0f172a",
                                        messageBorder: "#334155",
                                        anchorTextColor: "#60a5fa",
                                        dividerBackground: "#334155",
                                    },
                                    borderWidths: {
                                        buttonBorderWidth: "1px",
                                        inputBorderWidth: "1px",
                                    },
                                    radii: {
                                        borderRadiusButton: "8px",
                                        buttonBorderRadius: "8px",
                                        inputBorderRadius: "8px",
                                    },
                                },
                            },
                            style: {
                                button: {
                                    fontWeight: "600",
                                    fontFamily: "inherit",
                                },
                                input: {
                                    fontFamily: "inherit",
                                },
                                label: {
                                    fontFamily: "inherit",
                                    fontSize: "0.875rem",
                                },
                                anchor: {
                                    fontFamily: "inherit",
                                },
                                message: {
                                    fontFamily: "inherit",
                                },
                            },
                        }}
                        providers={["google"]}
                        redirectTo={
                            typeof window !== "undefined"
                                ? `${window.location.origin}/`
                                : "/"
                        }
                        socialLayout="horizontal"
                        localization={{
                            variables: {
                                sign_in: {
                                    email_label: "Email address",
                                    password_label: "Password",
                                    button_label: "Sign in",
                                    social_provider_text: "Continue with {{provider}}",
                                },
                                sign_up: {
                                    email_label: "Email address",
                                    password_label: "Create a password",
                                    button_label: "Create account",
                                    social_provider_text: "Sign up with {{provider}}",
                                },
                            },
                        }}
                    />
                </div>

                <p className="mt-6 text-center text-slate-600 text-xs">
                    By signing in, you agree to participate in good faith.
                </p>
            </div>
        </div>
    );
}
