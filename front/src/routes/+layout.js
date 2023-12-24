// This can be false if you're using a fallback (i.e. SPA mode)
export const prerender = true;
// Use this option such that the output build is in the expected format for fastapi static delivery
// https://stackoverflow.com/questions/76656259/how-do-i-route-subpages-correctly-with-fastapi
export const trailingSlash = 'always';