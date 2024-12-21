def calculate_cost(total_gb_per_day, compression_ratio=10, days_in_month=30):
    # Calculate total monthly uncompressed GB
    total_gb = total_gb_per_day * days_in_month
    
    # Apply the compression ratio to the total data size
    compressed_gb = total_gb / compression_ratio

    # Define the cost per GB for each tier
    free_tier = 100  # First 100 GB free
    tier_1_cost = 0.087  # Next 10 TB (10,240 GB)
    tier_2_cost = 0.083  # Next 40 TB (40,960 GB)
    tier_3_cost = 0.07   # Next 100 TB (102,400 GB)
    tier_4_cost = 0.05   # Next 350 TB (358,400 GB)

    # Initialize the allocation to the tiers for compressed data
    free_tier_used = min(compressed_gb, free_tier)
    remaining_gb_compressed = compressed_gb - free_tier_used

    tier_1_compressed = 0
    tier_2_compressed = 0
    tier_3_compressed = 0
    tier_4_compressed = 0

    # Allocate remaining GB to the respective tiers for compressed data
    if remaining_gb_compressed > 0:
        tier_1_compressed = min(remaining_gb_compressed, 10240)
        remaining_gb_compressed -= tier_1_compressed

    if remaining_gb_compressed > 0:
        tier_2_compressed = min(remaining_gb_compressed, 40960)
        remaining_gb_compressed -= tier_2_compressed

    if remaining_gb_compressed > 0:
        tier_3_compressed = min(remaining_gb_compressed, 102400)
        remaining_gb_compressed -= tier_3_compressed

    if remaining_gb_compressed > 0:
        tier_4_compressed = remaining_gb_compressed

    # Initialize the allocation to the tiers for uncompressed data
    free_tier_used_uncompressed = min(total_gb, free_tier)
    remaining_gb_uncompressed = total_gb - free_tier_used_uncompressed

    tier_1_uncompressed = 0
    tier_2_uncompressed = 0
    tier_3_uncompressed = 0
    tier_4_uncompressed = 0

    # Allocate remaining GB to the respective tiers for uncompressed data
    if remaining_gb_uncompressed > 0:
        tier_1_uncompressed = min(remaining_gb_uncompressed, 10240)
        remaining_gb_uncompressed -= tier_1_uncompressed

    if remaining_gb_uncompressed > 0:
        tier_2_uncompressed = min(remaining_gb_uncompressed, 40960)
        remaining_gb_uncompressed -= tier_2_uncompressed

    if remaining_gb_uncompressed > 0:
        tier_3_uncompressed = min(remaining_gb_uncompressed, 102400)
        remaining_gb_uncompressed -= tier_3_uncompressed

    if remaining_gb_uncompressed > 0:
        tier_4_uncompressed = remaining_gb_uncompressed

    # Calculate the cost for each tier for compressed data
    cost_tier_1_compressed = tier_1_compressed * tier_1_cost
    cost_tier_2_compressed = tier_2_compressed * tier_2_cost
    cost_tier_3_compressed = tier_3_compressed * tier_3_cost
    cost_tier_4_compressed = tier_4_compressed * tier_4_cost

    # Calculate the cost for each tier for uncompressed data
    cost_tier_1_uncompressed = tier_1_uncompressed * tier_1_cost
    cost_tier_2_uncompressed = tier_2_uncompressed * tier_2_cost
    cost_tier_3_uncompressed = tier_3_uncompressed * tier_3_cost
    cost_tier_4_uncompressed = tier_4_uncompressed * tier_4_cost

    # Total costs
    total_cost_compressed = cost_tier_1_compressed + cost_tier_2_compressed + cost_tier_3_compressed + cost_tier_4_compressed
    total_cost_uncompressed = cost_tier_1_uncompressed + cost_tier_2_uncompressed + cost_tier_3_uncompressed + cost_tier_4_uncompressed

    # Return the costs for each tier and the total cost
    return {
        'total_gb_per_day': total_gb_per_day,
        'total_gb_per_month': total_gb,
        'compressed_gb': compressed_gb,
        'compression_ratio': compression_ratio,
        'free_tier': free_tier_used,
        'tier_1_compressed': tier_1_compressed,
        'tier_2_compressed': tier_2_compressed,
        'tier_3_compressed': tier_3_compressed,
        'tier_4_compressed': tier_4_compressed,
        'cost_tier_1_compressed': cost_tier_1_compressed,
        'cost_tier_2_compressed': cost_tier_2_compressed,
        'cost_tier_3_compressed': cost_tier_3_compressed,
        'cost_tier_4_compressed': cost_tier_4_compressed,
        'total_cost_compressed': total_cost_compressed,
        'tier_1_uncompressed': tier_1_uncompressed,
        'tier_2_uncompressed': tier_2_uncompressed,
        'tier_3_uncompressed': tier_3_uncompressed,
        'tier_4_uncompressed': tier_4_uncompressed,
        'cost_tier_1_uncompressed': cost_tier_1_uncompressed,
        'cost_tier_2_uncompressed': cost_tier_2_uncompressed,
        'cost_tier_3_uncompressed': cost_tier_3_uncompressed,
        'cost_tier_4_uncompressed': cost_tier_4_uncompressed,
        'total_cost_uncompressed': total_cost_uncompressed
    }

# Example usage: For 1000 GB/day with a compression ratio of 10
total_gb_per_day = 7000  # Example: 1000 GB per day
compression_ratio = 10  # Default compression ratio
cost_details = calculate_cost(total_gb_per_day, compression_ratio)

# Print the results
print(f"Total GB (Uncompressed) per day: {cost_details['total_gb_per_day']}")
print(f"Total GB (Uncompressed) per month: {cost_details['total_gb_per_month']}")
print(f"Compressed GB (after ratio) per month: {cost_details['compressed_gb']}")
print(f"Compression Ratio: {cost_details['compression_ratio']}")
print(f"Free Tier: {cost_details['free_tier']}")
print(f"Tier 1 (Compressed): {cost_details['tier_1_compressed']}")
print(f"Tier 2 (Compressed): {cost_details['tier_2_compressed']}")
print(f"Tier 3 (Compressed): {cost_details['tier_3_compressed']}")
print(f"Tier 4 (Compressed): {cost_details['tier_4_compressed']}")
print(f"Cost for Tier 1 (Compressed): ${cost_details['cost_tier_1_compressed']:.2f}")
print(f"Cost for Tier 2 (Compressed): ${cost_details['cost_tier_2_compressed']:.2f}")
print(f"Cost for Tier 3 (Compressed): ${cost_details['cost_tier_3_compressed']:.2f}")
print(f"Cost for Tier 4 (Compressed): ${cost_details['cost_tier_4_compressed']:.2f}")
print(f"Total Monthly Cost (Compressed): ${cost_details['total_cost_compressed']:.2f}")
print(f"Tier 1 (Uncompressed): {cost_details['tier_1_uncompressed']}")
print(f"Tier 2 (Uncompressed): {cost_details['tier_2_uncompressed']}")
print(f"Tier 3 (Uncompressed): {cost_details['tier_3_uncompressed']}")
print(f"Tier 4 (Uncompressed): {cost_details['tier_4_uncompressed']}")
print(f"Cost for Tier 1 (Uncompressed): ${cost_details['cost_tier_1_uncompressed']:.2f}")
print(f"Cost for Tier 2 (Uncompressed): ${cost_details['cost_tier_2_uncompressed']:.2f}")
print(f"Cost for Tier 3 (Uncompressed): ${cost_details['cost_tier_3_uncompressed']:.2f}")
print(f"Cost for Tier 4 (Uncompressed): ${cost_details['cost_tier_4_uncompressed']:.2f}")
print(f"Total Monthly Cost (Uncompressed): ${cost_details['total_cost_uncompressed']:.2f}")
