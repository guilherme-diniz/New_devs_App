import React, { useCallback, useEffect, useState } from "react";
import { secureProperties } from "../lib/secureApi";

interface PropertySelectorProps {
  selectedPropertyId: string | null;
  onSelect: (propertyId: string | null) => void;
}

export const PropertySelector: React.FC<PropertySelectorProps> = ({
  selectedPropertyId,
  onSelect,
}) => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProperties = async () => {
      setLoading(true);
      try {
        const response = await secureProperties.getAll();
        setProperties(response.data);
      } catch (err) {
        setError("Failed to load properties");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProperties();
  }, []);

  const handleSelect = useCallback(
    (propertyId: string) => {
      onSelect(propertyId);
    },
    [onSelect],
  );

  return (
    <div className="flex flex-col sm:items-end">
      <label className="text-xs font-medium text-gray-700 mb-1">
        Select Property
      </label>
      {error && (
        <div className="p-4 text-red-500 bg-red-50 rounded-lg">{error}</div>
      )}
      {loading && (
        <div className="p-4 text-gray-500 bg-gray-50 rounded-lg">
          Loading properties...
        </div>
      )}
      {properties.length > 0 && (
        <select
          value={selectedPropertyId ?? undefined}
          onChange={(e) => handleSelect(e.target.value)}
          className="block w-full sm:w-auto min-w-[200px] px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
        >
          {properties.map((property) => (
            <option key={property.id} value={property.id}>
              {property.name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default PropertySelector;
