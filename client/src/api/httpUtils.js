// Utility to build fetch request body, automatically adding session token
export function buildRequestBody(httpParams = {}) {
  const sessionToken = sessionStorage.getItem("tempSessionToken");
  const body = {
    ...httpParams,
    session_token: sessionToken || null,
  };
  return JSON.stringify(body);
}
