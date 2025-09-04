function joinByteArrays(array1, array2) {
  const mergedArray = new Uint8Array(array1.length + array2.length);
  mergedArray.set(array1, 0);
  mergedArray.set(array2, array1.length);
  return mergedArray;
}

export const readFile = async (fileObject, setFile) => {
  if (!fileObject) {
    //console.log("No file selected.");
    return;
  }
  const stream = fileObject.stream();
  const reader = stream.getReader();
  let fullFileBytes = new Uint8Array(0);
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      //console.log("Stream reading complete.");
      setFile(fullFileBytes);
      return;
    }
    // Process the chunk of data
    //console.log("Chunk:", value);
    fullFileBytes = joinByteArrays(fullFileBytes, value);
  }
};
