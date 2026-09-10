# Cavrix AI — Deployment Guide

This document describes how to deploy the full Cavrix AI ecosystem.

## 1. Cavrix Web (Next.js)

The frontend is designed for seamless deployment on Vercel.

**Steps:**
1. Push the repository to GitHub.
2. Import the project in Vercel.
3. Set the required Environment Variables:
   - `NEXT_PUBLIC_GATEWAY_URL` (URL of the Realtime Gateway)
   - `DATABASE_URL` (Connection string for Postgres)
   - `NEXTAUTH_SECRET`
   - `GEMINI_API_KEY`
4. Deploy.

## 2. Realtime Gateway (WebSocket Server)

Since Vercel Serverless functions cannot maintain long-lived WebSockets, the Gateway must be deployed to a persistent container service (e.g., Render, Railway, Fly.io, or AWS Fargate).

**Steps:**
1. Provision a Node.js or Python container.
2. Expose the WSS port.
3. Configure Environment Variables:
   - `DATABASE_URL`
   - `GATEWAY_SECRET`
4. Deploy the container.

## 3. Cavrix Desktop Agent (Windows)

The local agent runs on the user's machine.

**Steps:**
1. Package the Python application (e.g., using PyInstaller) into a standalone `.exe`.
2. Provide an installer that registers the agent for auto-start.
3. On first launch, the user is prompted to input their Pairing Code generated from Cavrix Web.
4. The Agent saves the paired credentials securely in the Windows Credential Manager.

## 4. Environment Variables Checklist
- Never hardcode keys.
- Use `.env.local` for local development.
- Ensure all secrets are rotated regularly.
