'use client';

import * as TabsPrimitive from "@radix-ui/react-tabs";
import { cn } from "@/lib/utils"; // Utility for conditional classNames
import React from "react";

interface TabsProps extends TabsPrimitive.TabsProps {
  className?: string;
}

export function Tabs({ className = "", children, ...props }: TabsProps) {
  return (
    <TabsPrimitive.Root className={cn("w-full", className)} {...props}>
      {children}
    </TabsPrimitive.Root>
  );
}

interface TabsListProps extends TabsPrimitive.TabsListProps {
  className?: string;
}

export function TabsList({ className = "", ...props }: TabsListProps) {
  return (
    <TabsPrimitive.List className={cn("flex space-x-1 bg-gray-500 p-1 rounded-md", className)} {...props} />
  );
}

interface TabsTriggerProps extends TabsPrimitive.TabsTriggerProps {
  className?: string;
}

export function TabsTrigger({ className = "", ...props }: TabsTriggerProps) {
  return (
    <TabsPrimitive.Trigger
      className={cn(
        "px-4 py-2 font-medium text-sm rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
        "hover:bg-gray-300 data-[state=active]:bg-white data-[state=active]:shadow",
        className
      )}
      {...props}
    />
  );
}

interface TabsContentProps extends TabsPrimitive.TabsContentProps {
  className?: string;
}

export function TabsContent({ className = "", ...props }: TabsContentProps) {
  return (
    <TabsPrimitive.Content
      className={cn("mt-4 p-4 bg-gray-100 rounded-md shadow", className)}
      {...props}
    />
  );
} 