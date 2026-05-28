export default function Sidebar({ documents, onSelectDoc, onUpload }) {
  return (
    <div className="w-72 bg-gray-900 border-r border-gray-800 flex flex-col">
      {/* Upload Button */}
      <label className="p-4 border-b border-gray-800 cursor-pointer text-sm text-white bg-gray-800 hover:bg-gray-700">
        + Upload Document
        <input
          type="file"
          className="hidden"
          onChange={(e) => onUpload(e.target.files[0])}
        />
      </label>

      {/* Documents */}
      <div className="flex-1 overflow-y-auto">
        {documents.map((doc) => (
          <div
            key={doc.id}
            onClick={() => onSelectDoc(doc)}
            className="p-3 border-b border-gray-800 hover:bg-gray-800 cursor-pointer"
          >
            <p className="text-sm text-white truncate">{doc.filename}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
