export function get_storage_url(container, fileDir, fileName, sasURL = undefined) {
    const deployEnv = process.env.REACT_APP_DEPLOY_ENV
    if (deployEnv === "local") {
        return `${process.env.PUBLIC_URL}/${container}/${fileDir}/${fileName}`
    } else {
        if (sasURL !== undefined) {
            return sasURL
        } else{
            const name = process.env.REACT_APP_STORAGE_ACCOUNT_NAME
            const suffix = process.env.REACT_APP_STORAGE_ACCOUNT_SUFFIX
            return `https://${name}.${suffix}`
        }
    }
}