import React, { useState } from "react";
import PropertySelector from "./PropertySelector";
import { RevenueSummary } from "./RevenueSummary";

const Dashboard: React.FC = () => {
  const [selectedProperty, setSelectedProperty] = useState<string | null>(null);

  return (
    <div className="p-4 lg:p-6 min-h-full">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6 text-gray-900">
          Property Management Dashboard
        </h1>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 lg:p-6">
          <div className="mb-6">
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
              <div>
                <h2 className="text-lg lg:text-xl font-medium text-gray-900 mb-2">
                  Revenue Overview
                </h2>
                <p className="text-sm lg:text-base text-gray-600">
                  Monthly performance insights for your properties
                </p>
              </div>
              {/* Property Selector */}
              <PropertySelector
                selectedPropertyId={selectedProperty}
                onSelect={setSelectedProperty}
              />
            </div>
          </div>

          <div className="space-y-6">
            {selectedProperty && (
              <RevenueSummary propertyId={selectedProperty} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
