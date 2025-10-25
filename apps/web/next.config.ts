import type { NextConfig } from "next";

/**
 * Next.js configuration for Syntroph CRM
 * 
 * Open for collaboration: Add additional configuration as needed
 * - Image optimization domains
 * - Internationalization
 * - Redirects and rewrites
 */
const nextConfig: NextConfig = {
  // Enable standalone output for Docker production builds
  output: 'standalone',
  
  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  
  // Rewrites for API proxy (development)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ];
  },
  
  // TypeScript configuration
  typescript: {
    // Type checking happens in CI/CD pipeline
    ignoreBuildErrors: false,
  },
  
  // Experimental features
  experimental: {
    // Enable oRPC when implemented
    // serverActions: true,
  },
};

export default nextConfig;
