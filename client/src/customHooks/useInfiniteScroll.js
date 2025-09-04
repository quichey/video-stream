import { useState, useEffect, useRef, useCallback } from "react";
import { useServerCall } from "../customHooks/useServerCall";

export const useInfiniteScroll = ({
  route,
  initialParams = {},
  handleData,
  batchSize = 20,
}) => {
  const fetchServer = useServerCall();
  const sentinelRef = useRef(null);

  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;
    setLoading(true);

    try {
      const params = {
        ...initialParams,
        offset: page * batchSize,
        limit: batchSize,
      };
      const data = await fetchServer(route, handleData, params);

      if (data.length < batchSize) setHasMore(false);
      setPage((prev) => prev + 1);
      if (handleData) handleData(data);
    } catch (err) {
      console.error("Infinite scroll fetch failed", err);
    } finally {
      setLoading(false);
    }
  }, [
    fetchServer,
    route,
    page,
    loading,
    hasMore,
    batchSize,
    initialParams,
    handleData,
  ]);

  useEffect(() => {
    if (!sentinelRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) loadMore();
      },
      { rootMargin: "200px" }, // start loading before reaching bottom
    );

    observer.observe(sentinelRef.current);

    return () => observer.disconnect();
  }, [loadMore]);

  return { sentinelRef, loading, hasMore, loadMore };
};
