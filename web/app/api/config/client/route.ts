import { NextResponse } from 'next/server';

import configService from '@/services/ConfigService';

export async function GET() {
  try {
    const clientConfig = configService.getClientConfig();

    return NextResponse.json(await clientConfig, {
      headers: {
        'Cache-Control': 'public, max-age=300, s-maxage=300' // Cache age is in seconds
      }
    });
  } catch (error) {
    console.error('Error fetching client configuration:', error);
    return NextResponse.json(
      { error: 'Unable to fetch configuration' },
      { status: 500 }
    );
  }
}
