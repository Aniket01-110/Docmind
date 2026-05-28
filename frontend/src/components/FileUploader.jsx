export default function FileUploader({ onUpload, loading }) {
  return (
    <label className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm cursor-pointer">
      {loading ? "Uploading..." : "Upload"}
      <input
        type="file"
        className="hidden"
        onChange={(e) => onUpload(e.target.files[0])}
      />
    </label>
  );
}
