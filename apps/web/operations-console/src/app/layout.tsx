import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "LEP Operations Console",
  description: "Lysergic Engineering Platform Operations Console",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
