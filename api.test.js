const { fetchUserData } = require('./api');

// BUG 1: Missing assertion. The test runs but doesn't actually check anything.
test('it fetches user data successfully', () => {
    const data = { id: 1, name: 'Alice' };
    console.log("Mock data created:", data);
});

// BUG 2: Unawaited Promise. The test will complete and pass before the promise resolves or the assertion executes.
test('it fetches user data asynchronously', () => {
    fetchUserData(1).then(result => {
        expect(result.name).toBe('Alice');
    });
});
