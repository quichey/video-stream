export function get_storage_url(deployEnv) {
    if (deployEnv === "local") {
        return process.env.PUBLIC_URL
    } else {
        const name = process.env.REACT_APP_STORAGE_ACCOUNT_NAME
        const suffix = process.env.REACT_APP_STORAGE_ACCOUNT_SUFFIX
        return `https://${name}.${suffix}`
    }
}