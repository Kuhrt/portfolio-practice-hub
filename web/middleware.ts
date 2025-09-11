import { NextResponse } from 'next/server';
import { HEADER_PATHNAME } from '@/constants/header';
import { auth as authMiddleware } from '@/utils/auth';

export const AUTH_PAGES = ['/login', '/logout', '/logged-out', '/login/error'];
export const UNPROTECTED_PAGES = ['/unauthorized', ...AUTH_PAGES];

export default authMiddleware(async (req) => {
  const { nextUrl, auth: session } = req;

  // * If auth should be enforced
  if (!UNPROTECTED_PAGES.includes(nextUrl.pathname)) {
    // * Redirect to login page if not authenticated or if the token has some error
    if (!session || !!session.tokenError) {
      const searchParams = new URLSearchParams(nextUrl.searchParams);
      searchParams.set('next', nextUrl.pathname);
      const newUrl = new URL(`/login?${searchParams}`, nextUrl.origin);
      return NextResponse.redirect(newUrl);
    }

    // Check page-specific role requirements
    // const userRoles = session.user?.roles || [];
    // const path = nextUrl.pathname.split('/')[1];
    // const requiredRole = rolePathsMap.get(path || '');

    // if (!!requiredRole && !hasPermission(userRoles, [requiredRole])) {
    //   return NextResponse.redirect(new URL('/unauthorized', nextUrl.origin));
    // }
  }

  // * Custom headers
  const requestHeaders = new Headers(req.headers);
  requestHeaders.set(HEADER_PATHNAME, req.nextUrl.pathname);

  return NextResponse.next({
    request: {
      headers: requestHeaders
    }
  });
});

export const config = {
  // * Add to the regex to exclude paths from the middleware
  // * Current: API Routes | Static Folder | _next Folders | Public Folder (anything with a dot in the name for images, etc)
  matcher: ['/((?!api|static|_next|.*\\..*).*)']
};
