/**
 * Calculates the standard deviation of an array of numbers.
 * 
 * @param values - An array of numbers.
 * @returns The standard deviation of the given numbers.
 * @throws Will throw an error if the array is empty.
 */
export function calculateStandardDeviation(values: number[]): number {
    if (!Array.isArray(values) || values.length === 0) {
        throw new Error("Input must be a non-empty array of numbers.");
    }

    const n = values.length;
    const mean = values.reduce((sum, value) => sum + value, 0) / n;
    
    const squaredDifferences = values.map(value => {
        const diff = value - mean;
        return diff * diff;
    });

    const variance = squaredDifferences.reduce((sum, squaredDiff) => sum + squaredDiff, 0) / n;
    
    return Math.sqrt(variance);
}

/**
 * Formats a given number as a currency string.
 * 
 * @param amount - The number to format.
 * @param currencyCode - The ISO 4217 currency code (e.g., 'USD', 'EUR'). Default is 'USD'.
 * @param locale - The locale string (e.g., 'en-US', 'de-DE'). Default is 'en-US'.
 * @returns The formatted currency string.
 */
export function formatCurrency(amount: number, currencyCode: string = 'USD', locale: string = 'en-US'): string {
    if (typeof amount !== 'number' || isNaN(amount)) {
        throw new Error("Amount must be a valid number.");
    }

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currencyCode,
    }).format(amount);
}
