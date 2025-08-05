from cloud_providers.azure_provider import AzureProvider

COST_THRESHOLD = 100.0  # USD

def rank_services_by_cost(provider):
    services = provider.fetch_services()
    ranked = []
    for service in services:
        cost = provider.fetch_costs(service)
        ranked.append((service, cost))
    ranked.sort(key=lambda x: x[1], reverse=True)

    print("\nRanked Services by Cost:")
    for service, cost in ranked:
        print(f"Service: {service['name']} | ID: {service['id']} | Cost: ${cost:.2f}")
    return ranked

def close_wasteful_services(provider, services_with_costs):
    for service, cost in services_with_costs:
        if cost > COST_THRESHOLD:
            print(f"Service {service['name']} exceeds threshold (${cost:.2f}). Shutting down...")
            provider.shut_down(service)
        else:
            print(f"Service {service['name']} is within cost threshold (${cost:.2f}).")

def main():
    provider = AzureProvider()
    ranked_services = rank_services_by_cost(provider)
    close_wasteful_services(provider, ranked_services)

if __name__ == "__main__":
    main()
