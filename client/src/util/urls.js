export function get_storage_url(deployEnv) {
    if (deployEnv === "local") {
        return process.env.PUBLIC_URL
    } else {
        return `https://${process.env.REACT_APP_STORAGE_ACCOUNT_NAME}.blob.core.windows.net`
    }
}